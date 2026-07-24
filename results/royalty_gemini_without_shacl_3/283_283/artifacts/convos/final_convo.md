================================ System Message ================================

### Role
You are an expert Knowledge Graph Engineer. Your task is to update and refine a Data Graph based on a provided Input Text and a strict Ontology. You must ensure the Data Graph accurately reflects the information in the text while remaining compliant with the ontological constraints.

### Inputs
1. **Ontology**: Allowed classes and properties.
2. **Input Text**: The ONLY source of truth.
3. **Current Data Graph**: The starting state.

### Strict Grounding & Scope
- **No External Knowledge**: You are a "clean slate" engineer. Even if you know more about the subject from your training data, you MUST NOT add any node or relation that is not explicitly mentioned in the **Input Text**.
- **No Hypothetical Nodes**: Do not create placeholder nodes or sequences (e.g., Marriage1, Marriage2) to represent "patterns" mentioned in the text. Only create nodes for specific instances described.
- **Quantities**: If the text says "fifteen children" but does not name them, do NOT create 15 generic child nodes. Only create nodes for entities with specific names or identifiers provided in the text.

### Triadic Directionality & Predicate Logic (STRICT ENFORCEMENT)
The Data Graph is a **Directed Acyclic Graph**. Swapping Source and Target is a critical failure that invalidates the entire graph. You MUST follow the **Flow of Action**.

#### 1. The "Sentence Test" Requirement
Before executing any `AddTriple` call, you must mentally or explicitly (in your thought process) perform the following test:
* **Formula**: `[Source Entity] + [Property Name] + [Target Entity]`
* **Check**: Does this form a grammatically and logically correct sentence based *only* on the text?
* **Example Failure**: If the text says "John is the employer of Mary," the triple `(Mary, isEmployerOf, John)` fails because "Mary isEmployerOf John" is factually false.

#### 2. Identifying the Anchor (Domain vs. Range)
* **The Source**: The "Origin" or "Owner." If the property is a verb, the Source is the one performing it. Source is always to the left of a relation.
* **The Target**: The "Destination" or "Attribute." If the property is a verb, the Target is the one being acted upon. Target is always to the right of a relation.

#### 3. Handling Inverse Property Confusion
Many errors occur because the LLM confuses a relation with its inverse. You must be hyper-vigilant:
* **Active (`worksFor`, `isEmployerOf`)**: The "Superior" or "Source" is the Source.
* **Passive (`employedBy`, `childOf`)**: The "Subordinate" or "Recipient" is the Source.
* **Partitive (`hasPart`, `contains`)**: The "Container/Whole" is the Source.
* **Membership (`isPartOf`, `memberOf`)**: The "Component/Part" is the Source.

#### 4. Negative Constraints
* **NEVER** use the property name as a bidirectional link.
* **NEVER** assume the first entity mentioned in a sentence is automatically the Source; analyze the verb direction.

#### 5. Arguments Order
* When calling `AddTriple` `source` **ALWAYS** comes first, then `relation`, and only after them `target`.

> **STOP & VERIFY**: If your triple reads like "Employee isEmployerOf Employer" or "Room contains Building," you have flipped the nodes. **STOP and swap them before calling the tool.**


### Naming Conventions
- **Identifiers**: Use semantic identifiers derived from the text. 
- **Avoid Numbering**: Do not use arbitrary numbers unless that specific number appears in the text in relation to that entity.
- **Inclusion of Titles**: Retain all regnal numbers, honorary prefixes, or noble titles if they are part of the primary identifying name (e.g., "Crown Prince [Name]" or "[Name] II").
- **Territorial Origins**: If a person is identified by their house, dynasty, or place of origin as part of their formal name, include the full "of [Location]" or "[Location-Suffix]" descriptor.
- **Avoid Pronouns/Aliases**: Never use pronouns or shortened versions of the name mentioned later in the text. Always map back to the most complete version of the name found within the source material.

### Instructions & Workflow
1. **Analyze**: Identify specific entities and relations in the text.
2. **Edit**: Use tools to modify the graph.
   - Every node MUST have a class assignment (`AssignClass`).
   - Ground every edit in text evidence.
3. **Finalize**: Use `Finish` once the graph is a **faithful** representation of the text.

### Tool Usage Constraints
- **AssignClass / UnassignClass**: For `rdf:type` only.
- **AddTriple / RemoveTriple**: For properties only.
- **AddLiteral / RemoveLiteral**: For literals (raw data: dates, numbers, strings, etc.) only.
- **Finish**: Once you are finished, use this tool.
- **Batching**: You may use multiple tools, but **DON'T EXCEED 20 TOOL CALLS IN A SINGLE ANSWER**. Focus on quality and grounding over quantity.

================================ Human Message =================================

Please update the Knowledge Graph based on the provided data.

### Input Text:
Prince Louis of Wales (/ˈluːi/ LOO-ee; Louis Arthur Charles; born 23 April 2018) is a member of the British royal family.
He is the third and youngest child of William, Prince of Wales, and Catherine, Princess of Wales, and a grandson of King Charles III and Diana, Princess of Wales.
Infancy

Louis was born at 11:01 am on 23 April 2018 at St Mary's Hospital, London, during the reign of his paternal great-grandmother, Queen Elizabeth II.
He is the third child and second son of Prince William and Catherine (then known as Duke and Duchess of Cambridge).
He has an elder brother and sister, Prince George and Princess Charlotte.
On 27 April, his name was announced as Louis Arthur Charles, honouring his paternal grandfather, Charles, Prince of Wales (later King Charles  III) and his 3rd-great-uncle Louis, Earl Mountbatten of Burma.
Louis was christened on 9 July by the archbishop of Canterbury, Justin Welby, in the Chapel Royal at St James's Palace.
Upbringing

Louis and his family lived at Kensington Palace and Anmer Hall in Norfolk during his early childhood.
Louis accompanied his siblings and parents to Elizabeth II's Platinum Jubilee celebrations in June 2022.
Elizabeth II died on 8 September 2022 and Louis's grandfather became king.
Accordingly, Louis became fourth in line to the throne.
Title and style

Louis is a British prince with the official style and title "His Royal Highness Prince Louis of Wales".
Before his father was created Prince of Wales on 9 September 2022, Louis was styled "His Royal Highness Prince Louis of Cambridge".
Succession

Louis is fourth in the line of succession to the British throne, behind his father and his two elder siblings.
Following the implementation of the Perth Agreement, which replaced male-preference primogeniture with absolute primogeniture, he is the first British prince to be ranked behind an elder sister in the line of succession.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://www.w3.org/2003/11/swrl#> .
@prefix ns2: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

: a owl:Ontology ;
    dcterms:source <http://www.co-ode.org/roberts/family-tree.owl> .

:alsoKnownAs a owl:AnnotationProperty .

:formerlyKnownAs a owl:AnnotationProperty .

:hasBirthYear a rdfs:Datatype,
        owl:AnnotationProperty .

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

:isAuntOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isSisterOf :isParentOf ) .

:isUncleOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isBrotherOf :isParentOf ) .

:knownAs a owl:AnnotationProperty .

dcterms:source a owl:AnnotationProperty .

ns2:isRuleEnabled a owl:AnnotationProperty .

:hasBrother a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isBrotherOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasDaughter a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isDaughterOf .

:hasFather a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Man ;
    rdfs:subPropertyOf :hasParent ;
    owl:inverseOf :isFatherOf .

:hasMother a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Woman ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf ;
    owl:inverseOf :isMotherOf .

:hasSister a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isSisterOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasSon a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isSonOf .

:isBloodrelationOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty .

:isDaughterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:isFatherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isMotherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isSonOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:DomainEntity a owl:Class .

:Female a owl:Class ;
    rdfs:subClassOf :Sex ;
    owl:disjointWith :Male .

:hasAncestor a owl:ObjectProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty ;
    owl:inverseOf :isAncestorOf .

:isBrotherOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:Male a owl:Class ;
    rdfs:subClassOf :Sex .

:hasRelation a owl:ObjectProperty,
        owl:SymmetricProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person .

:hasSex a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Sex .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:x a ns1:Variable .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:y a ns1:Variable .

:Ancestor a owl:Class ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :isAncestorOf ;
                        owl:someValuesFrom :Person ] ) ] .

:Person a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:onProperty :hasFather ;
            owl:someValuesFrom :Man ],
        [ a owl:Restriction ;
            owl:onProperty :hasMother ;
            owl:someValuesFrom :Woman ],
        [ a owl:Restriction ;
            owl:onProperty :hasSex ;
            owl:someValuesFrom :Sex ],
        [ a owl:Restriction ;
            owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
            owl:onClass :Person ;
            owl:onProperty :hasParent ],
        :DomainEntity ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Man :Woman ) ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSon" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasBrother" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSister" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (73d62678-9a30-4fb9-acc7-3bbcfd72f25b)
 Call ID: 73d62678-9a30-4fb9-acc7-3bbcfd72f25b
  Args:
    type: :Man
    source: :PrinceLouisOfWales
  AssignClass (8e722a70-a47b-486a-afd5-fa190681eab3)
 Call ID: 8e722a70-a47b-486a-afd5-fa190681eab3
  Args:
    type: :Person
    source: :PrinceLouisOfWales
  AddLiteral (73b9035b-d5dc-4d9a-bb05-a0a819702a42)
 Call ID: 73b9035b-d5dc-4d9a-bb05-a0a819702a42
  Args:
    relation: :hasBirthYear
    literal_value: 2018
    source: :PrinceLouisOfWales
    literal_type: xsd:integer
  AssignClass (37ff4119-0e95-497a-b126-63fbc8c7ecdd)
 Call ID: 37ff4119-0e95-497a-b126-63fbc8c7ecdd
  Args:
    type: :Man
    source: :PrinceWilliam
  AssignClass (93019c04-d45b-42d6-ab88-46094d077ab5)
 Call ID: 93019c04-d45b-42d6-ab88-46094d077ab5
  Args:
    type: :Person
    source: :PrinceWilliam
  AssignClass (f06940f1-5260-404b-9c75-b59daf022670)
 Call ID: f06940f1-5260-404b-9c75-b59daf022670
  Args:
    type: :Woman
    source: :CatherinePrincessOfWales
  AssignClass (08dfb625-6bfd-4512-b493-7bb012e84765)
 Call ID: 08dfb625-6bfd-4512-b493-7bb012e84765
  Args:
    type: :Person
    source: :CatherinePrincessOfWales
  AddTriple (4a0b0d75-6494-498f-bf0b-c50a36ef67ac)
 Call ID: 4a0b0d75-6494-498f-bf0b-c50a36ef67ac
  Args:
    target: :PrinceWilliam
    relation: :hasFather
    source: :PrinceLouisOfWales
  AddTriple (9ab1f4eb-978f-4322-9957-952fc19d04c5)
 Call ID: 9ab1f4eb-978f-4322-9957-952fc19d04c5
  Args:
    target: :CatherinePrincessOfWales
    source: :PrinceLouisOfWales
    relation: :hasMother
  AssignClass (2eb9239d-2702-4392-b86f-b3e86faca009)
 Call ID: 2eb9239d-2702-4392-b86f-b3e86faca009
  Args:
    type: :Man
    source: :KingCharlesIII
  AssignClass (3ca81d2a-dc2e-4948-8396-7b92b9847fd1)
 Call ID: 3ca81d2a-dc2e-4948-8396-7b92b9847fd1
  Args:
    type: :Person
    source: :KingCharlesIII
  AssignClass (f659640f-2627-4bb6-97d3-7aae80adc651)
 Call ID: f659640f-2627-4bb6-97d3-7aae80adc651
  Args:
    type: :Woman
    source: :DianaPrincessOfWales
  AssignClass (5f6637ca-da23-4b59-99ac-234e1f5d49ae)
 Call ID: 5f6637ca-da23-4b59-99ac-234e1f5d49ae
  Args:
    type: :Person
    source: :DianaPrincessOfWales
  AddTriple (4811a626-668d-4f61-8acc-66f048089d6e)
 Call ID: 4811a626-668d-4f61-8acc-66f048089d6e
  Args:
    target: :KingCharlesIII
    relation: :hasFather
    source: :PrinceWilliam
  AddTriple (66adb908-d38b-46e5-8be9-78b25415c2c6)
 Call ID: 66adb908-d38b-46e5-8be9-78b25415c2c6
  Args:
    target: :DianaPrincessOfWales
    relation: :hasMother
    source: :PrinceWilliam
  AssignClass (42956642-f570-4b09-9b8a-e89f76cdb55c)
 Call ID: 42956642-f570-4b09-9b8a-e89f76cdb55c
  Args:
    type: :Man
    source: :PrinceGeorge
  AssignClass (db68ebfc-fe99-4aa8-a6e6-afaadc494fd9)
 Call ID: db68ebfc-fe99-4aa8-a6e6-afaadc494fd9
  Args:
    type: :Person
    source: :PrinceGeorge
  AssignClass (2de4d97e-dacc-4407-b2f6-d13e5d344925)
 Call ID: 2de4d97e-dacc-4407-b2f6-d13e5d344925
  Args:
    type: :Woman
    source: :PrincessCharlotte
  AssignClass (5dbac335-ff35-4474-b380-e1cd26bd5310)
 Call ID: 5dbac335-ff35-4474-b380-e1cd26bd5310
  Args:
    type: :Person
    source: :PrincessCharlotte
  AddTriple (60e79dbc-764a-440a-b050-e3523d4f5b41)
 Call ID: 60e79dbc-764a-440a-b050-e3523d4f5b41
  Args:
    target: :PrinceGeorge
    source: :PrinceLouisOfWales
    relation: :isSiblingOf
  AddTriple (0fda7c59-d36b-4f22-876b-4301b5046b93)
 Call ID: 0fda7c59-d36b-4f22-876b-4301b5046b93
  Args:
    target: :PrincessCharlotte
    source: :PrinceLouisOfWales
    relation: :isSiblingOf
  AddTriple (7bdba498-0fa9-4133-8f69-d4e1e847845e)
 Call ID: 7bdba498-0fa9-4133-8f69-d4e1e847845e
  Args:
    target: :PrinceWilliam
    relation: :hasFather
    source: :PrinceGeorge
  AddTriple (9a385e74-4713-4b96-aaa0-de1ef467893b)
 Call ID: 9a385e74-4713-4b96-aaa0-de1ef467893b
  Args:
    target: :CatherinePrincessOfWales
    source: :PrinceGeorge
    relation: :hasMother
  AddTriple (a38be8ca-19de-4c36-ae5d-e2dffad07bbe)
 Call ID: a38be8ca-19de-4c36-ae5d-e2dffad07bbe
  Args:
    source: :PrincessCharlotte
    relation: :hasFather
    target: :PrinceWilliam
  AddTriple (2b765aaf-1262-4b83-9eb2-896dbebc1d25)
 Call ID: 2b765aaf-1262-4b83-9eb2-896dbebc1d25
  Args:
    target: :CatherinePrincessOfWales
    source: :PrincessCharlotte
    relation: :hasMother
  Finish (ed5a20b0-8a5f-4e19-b60e-d32de62db0d1)
 Call ID: ed5a20b0-8a5f-4e19-b60e-d32de62db0d1
  Args: