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
Princess Charlotte of Wales (Charlotte Elizabeth Diana; born 2 May 2015) is a member of the British royal family.
She is the second child and only daughter of William, Prince of Wales, and Catherine, Princess of Wales, and a granddaughter of King Charles III and Diana, Princess of Wales.
Infancy

Charlotte was born at 8:34 am on 2 May 2015 at St Mary's Hospital, London, during the reign of her paternal great-grandmother, Queen Elizabeth II.
She is the second child and only daughter of Prince William and Catherine (then known as Duke and Duchess of Cambridge).
She has an older and younger brother, Prince George and Prince Louis.
On 4 May her name was announced as Charlotte Elizabeth Diana, honouring her grandfather Charles, her great-grandmother, and her grandmother Diana.
Charlotte was christened on 5 July by the archbishop of Canterbury, Justin Welby, at St Mary Magdalene Church, Sandringham.
Upbringing

The family lived at Anmer Hall in Norfolk during Charlotte's infancy, before relocating to Kensington Palace in 2017.
Charlotte started at Willcocks Nursery School in January 2018.
She joined George at Thomas's School in Battersea in September 2019, where she was known as Charlotte Cambridge.
Following the death of Elizabeth II on 8 September 2022, Charlotte's grandfather acceded to the throne as Charles III, and Charlotte became third in line to the throne.
Public image

Despite the efforts of her parents to keep their children from public view, photographs and public appearances of Charlotte continue to attract media attention.
Shopping statistics and polls among parents show that Charlotte is a major children's style icon.
Title and styles

Charlotte is a British princess with the official style and title "Her Royal Highness Princess Charlotte of Wales".
Before her father was created Prince of Wales on 9 September 2022, Charlotte was styled "Her Royal Highness Princess Charlotte of Cambridge".
Succession

Charlotte is third in the line of succession to the British throne, behind her father and elder brother.
Because of the implementation of the Perth Agreement, which replaced male-preference primogeniture with absolute primogeniture, she did not move down the line of succession upon the birth of her younger brother Louis in April 2018, making her the first British princess in history to rank above a brother in the line of succession.



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
  AssignClass (cef8bd19-63c3-4f52-bf69-b5d94c35eff6)
 Call ID: cef8bd19-63c3-4f52-bf69-b5d94c35eff6
  Args:
    source: :Charlotte_of_Wales
    type: :Person
  AssignClass (ee04fc35-7eb7-4b6f-ae7b-077e93b695e9)
 Call ID: ee04fc35-7eb7-4b6f-ae7b-077e93b695e9
  Args:
    source: :Charlotte_of_Wales
    type: :Woman
  AddLiteral (50cebccd-8d2b-49ca-8846-d6756c8e802c)
 Call ID: 50cebccd-8d2b-49ca-8846-d6756c8e802c
  Args:
    relation: :hasBirthYear
    literal_value: 2015
    literal_type: xsd:integer
    source: :Charlotte_of_Wales
  AddLiteral (c337e517-d078-4c41-b19e-47ad91e9d833)
 Call ID: c337e517-d078-4c41-b19e-47ad91e9d833
  Args:
    literal_type: xsd:string
    source: :Charlotte_of_Wales
    literal_value: Charlotte Elizabeth Diana
    relation: :alsoKnownAs
  AddLiteral (45f4f816-253a-4ffe-b522-a695103777ef)
 Call ID: 45f4f816-253a-4ffe-b522-a695103777ef
  Args:
    literal_value: Charlotte Cambridge
    relation: :alsoKnownAs
    source: :Charlotte_of_Wales
    literal_type: xsd:string
  AssignClass (13e44db9-3b48-455a-a095-89fcbbd362a5)
 Call ID: 13e44db9-3b48-455a-a095-89fcbbd362a5
  Args:
    type: :Person
    source: :William_Prince_of_Wales
  AssignClass (d70b3cb1-509d-45e3-8257-169a3fce25bf)
 Call ID: d70b3cb1-509d-45e3-8257-169a3fce25bf
  Args:
    type: :Man
    source: :William_Prince_of_Wales
  AssignClass (07bb801d-f051-4380-997d-1c9db126e47e)
 Call ID: 07bb801d-f051-4380-997d-1c9db126e47e
  Args:
    source: :Catherine_Princess_of_Wales
    type: :Person
  AssignClass (06c0854e-fe94-4e3c-be48-debc3844534b)
 Call ID: 06c0854e-fe94-4e3c-be48-debc3844534b
  Args:
    type: :Woman
    source: :Catherine_Princess_of_Wales
  AddTriple (fda7879e-3ddf-43f0-a393-f86b6bdeba43)
 Call ID: fda7879e-3ddf-43f0-a393-f86b6bdeba43
  Args:
    source: :Charlotte_of_Wales
    relation: :hasFather
    target: :William_Prince_of_Wales
  AddTriple (2ec2878f-1e0a-49e6-b1fb-e8afd95ba61f)
 Call ID: 2ec2878f-1e0a-49e6-b1fb-e8afd95ba61f
  Args:
    source: :Charlotte_of_Wales
    relation: :hasMother
    target: :Catherine_Princess_of_Wales
  AssignClass (6da26b29-0195-4ccd-b4de-0b6e0686b75a)
 Call ID: 6da26b29-0195-4ccd-b4de-0b6e0686b75a
  Args:
    type: :Person
    source: :Charles_III
  AssignClass (d6eef642-4e39-4ae4-8069-79dea1e17e05)
 Call ID: d6eef642-4e39-4ae4-8069-79dea1e17e05
  Args:
    type: :Man
    source: :Charles_III
  AssignClass (4a0fe4ac-7a36-4075-ab3d-913850a69282)
 Call ID: 4a0fe4ac-7a36-4075-ab3d-913850a69282
  Args:
    source: :Diana_Princess_of_Wales
    type: :Person
  AssignClass (d08bef66-07c2-405d-8cdf-fae7be6383ec)
 Call ID: d08bef66-07c2-405d-8cdf-fae7be6383ec
  Args:
    type: :Woman
    source: :Diana_Princess_of_Wales
  AddTriple (2779939d-238e-4ef0-b045-764fa4472714)
 Call ID: 2779939d-238e-4ef0-b045-764fa4472714
  Args:
    source: :William_Prince_of_Wales
    target: :Charles_III
    relation: :hasFather
  AddTriple (6c69f561-ca25-4f21-8835-826e66005671)
 Call ID: 6c69f561-ca25-4f21-8835-826e66005671
  Args:
    target: :Diana_Princess_of_Wales
    relation: :hasMother
    source: :William_Prince_of_Wales
  AssignClass (a028d8fc-e3c2-46ed-a93b-d37ac40d0104)
 Call ID: a028d8fc-e3c2-46ed-a93b-d37ac40d0104
  Args:
    source: :Prince_George
    type: :Person
  AssignClass (118ae682-cb06-4a44-bf8a-8f2611a4aa9c)
 Call ID: 118ae682-cb06-4a44-bf8a-8f2611a4aa9c
  Args:
    type: :Man
    source: :Prince_George
  AssignClass (b915f5b7-483d-41cf-94a1-7047ba0a65d9)
 Call ID: b915f5b7-483d-41cf-94a1-7047ba0a65d9
  Args:
    type: :Person
    source: :Prince_Louis
  AssignClass (42386a93-4e40-4a12-885a-175a352d4f57)
 Call ID: 42386a93-4e40-4a12-885a-175a352d4f57
  Args:
    type: :Man
    source: :Prince_Louis
  AddTriple (497fd773-2935-4563-9714-bfe3660efee4)
 Call ID: 497fd773-2935-4563-9714-bfe3660efee4
  Args:
    relation: :isSiblingOf
    target: :Prince_George
    source: :Charlotte_of_Wales
  AddTriple (2ea67dbd-3b37-4914-aee0-2672529831d7)
 Call ID: 2ea67dbd-3b37-4914-aee0-2672529831d7
  Args:
    source: :Charlotte_of_Wales
    relation: :isSiblingOf
    target: :Prince_Louis
  AssignClass (659bd150-e012-4cd8-b133-371973432fdb)
 Call ID: 659bd150-e012-4cd8-b133-371973432fdb
  Args:
    type: :Person
    source: :Elizabeth_II
  AssignClass (1d3fc09a-c7f3-479e-b60b-057224c5f4af)
 Call ID: 1d3fc09a-c7f3-479e-b60b-057224c5f4af
  Args:
    source: :Elizabeth_II
    type: :Woman
  Finish (1ca2d237-84b3-459a-a0f6-e63606255516)
 Call ID: 1ca2d237-84b3-459a-a0f6-e63606255516
  Args: