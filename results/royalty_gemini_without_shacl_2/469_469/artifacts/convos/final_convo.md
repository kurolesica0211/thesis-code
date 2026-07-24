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
Countess Walburga Douglas (née von Habsburg-Lothringen; born 5 October 1958) is a German-born Swedish lawyer and politician, who served as a member of the Riksdag of Sweden for the Moderate Party from 2006 to 2014.
Early life

Born in 1958 in Berg am Starnberger See, West Germany, she is the fifth daughter of Otto von Habsburg, the last crown prince of Austria-Hungary, and his wife Princess Regina of Saxe-Meiningen.
Walburga was banished from the Republic of Austria from birth and well into adult life, along with her siblings, by the Habsburg Law that had been in effect since 1938, having been (re)imposed by the Nazis.
She is a granddaughter of the last Austrian emperor, Charles I, and a member of the House of Habsburg-Lorraine.
Her ancestral titles (abolished in Austria since 1919) are Archduchess Walburga of Austria, Archduchess of Austria, Princess of Hungary and Bohemia, with the style of Her Imperial and Royal Highness (HI&RH).
She does not currently use her ancestral titles actively in her daily life; however, by law she holds the title of Countess Douglas in the Kingdom of Sweden, her current country of residence and citizenship.
On 17 September 2023, Douglas visited Armenia to dedicate the opening of the PanEuropa Armenia branch in Yerevan.
Personal life

On 5 December 1992 in Budapest, Hungary, Walburga married a Swedish nobleman, Count Carl Axel Archibald Douglas (born 27 November 1949 in Stockholm), son of Count Archibald Douglas and Baroness Margareta Lagerfelt.
Her husband's family is a  noble family in Sweden, descended from the Scot Robert Douglas, Count of Skenninge, member of the Scottish Clan Douglas and founder of its Swedish branch.
Her husband is a first cousin of Count Gustaf Douglas and his sisters Rosita Spencer-Churchill, Duchess of Marlborough, and Princess Elisabeth, Duchess in Bavaria, the wife of Prince Max, Duke in Bavaria.
They have a son, Count Mauritz Otto Wenzel Douglas (born 30 March 1994 in Stockholm).



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix ns2: <http://www.w3.org/2003/11/swrl#> .
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

ns1:isRuleEnabled a owl:AnnotationProperty .

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

:x a ns2:Variable .

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

:y a ns2:Variable .

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

[] a ns2:Imp ;
    rdfs:label "infer hasSon" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasBrother" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSister" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (b58efb98-8c74-4cd6-b92b-809b57895118)
 Call ID: b58efb98-8c74-4cd6-b92b-809b57895118
  Args:
    type: :Woman
    source: WalburgaDouglas
  AssignClass (31ecf7d4-079a-44ca-a4a1-761de551704d)
 Call ID: 31ecf7d4-079a-44ca-a4a1-761de551704d
  Args:
    type: :Person
    source: WalburgaDouglas
  AddLiteral (9d25c5b9-b667-4e5a-a7bf-c9947669e11b)
 Call ID: 9d25c5b9-b667-4e5a-a7bf-c9947669e11b
  Args:
    literal_value: 1958
    source: WalburgaDouglas
    relation: :hasBirthYear
    literal_type: xsd:integer
  AssignClass (e1513a99-992a-4344-bc0a-370dbb22a5d0)
 Call ID: e1513a99-992a-4344-bc0a-370dbb22a5d0
  Args:
    type: :Man
    source: OttoVonHabsburg
  AssignClass (e5325841-274a-46fa-9f2e-a93396cb643e)
 Call ID: e5325841-274a-46fa-9f2e-a93396cb643e
  Args:
    source: OttoVonHabsburg
    type: :Person
  AssignClass (7c2bb546-abd3-4876-92cb-348438b04cf0)
 Call ID: 7c2bb546-abd3-4876-92cb-348438b04cf0
  Args:
    source: OttoVonHabsburg
    type: :Ancestor
  AssignClass (20774fcc-9530-43f9-9d51-700b7e8774ea)
 Call ID: 20774fcc-9530-43f9-9d51-700b7e8774ea
  Args:
    source: ReginaOfSaxeMeiningen
    type: :Woman
  AssignClass (881fbd1e-79bd-41c5-a112-d3e0e0d124fd)
 Call ID: 881fbd1e-79bd-41c5-a112-d3e0e0d124fd
  Args:
    source: ReginaOfSaxeMeiningen
    type: :Person
  AssignClass (5020055c-6a34-4197-bf50-16dfde6900b5)
 Call ID: 5020055c-6a34-4197-bf50-16dfde6900b5
  Args:
    source: ReginaOfSaxeMeiningen
    type: :Ancestor
  AddTriple (44b73736-6605-4136-9a7d-ba7865e61452)
 Call ID: 44b73736-6605-4136-9a7d-ba7865e61452
  Args:
    relation: :hasFather
    target: OttoVonHabsburg
    source: WalburgaDouglas
  AddTriple (ecca4fe9-1538-4b68-addb-6238324236d0)
 Call ID: ecca4fe9-1538-4b68-addb-6238324236d0
  Args:
    source: WalburgaDouglas
    target: ReginaOfSaxeMeiningen
    relation: :hasMother
  AssignClass (49a7eedc-227e-4981-bdd5-903b7f6cd29d)
 Call ID: 49a7eedc-227e-4981-bdd5-903b7f6cd29d
  Args:
    source: CharlesI
    type: :Man
  AssignClass (6172002f-0a13-4680-89f9-d74409365bfe)
 Call ID: 6172002f-0a13-4680-89f9-d74409365bfe
  Args:
    type: :Person
    source: CharlesI
  AssignClass (47d6f1fb-09ec-47c2-9ed0-40a61a651869)
 Call ID: 47d6f1fb-09ec-47c2-9ed0-40a61a651869
  Args:
    source: CharlesI
    type: :Ancestor
  AddTriple (eea028c5-5a67-469f-a64f-be3b7636b31d)
 Call ID: eea028c5-5a67-469f-a64f-be3b7636b31d
  Args:
    source: WalburgaDouglas
    target: CharlesI
    relation: :hasAncestor
  AssignClass (00e58d59-c7cb-4d92-bad8-dec561e8eaa2)
 Call ID: 00e58d59-c7cb-4d92-bad8-dec561e8eaa2
  Args:
    source: CarlAxelArchibaldDouglas
    type: :Man
  AssignClass (5573368b-c479-4d0f-b5be-97abc8c8d0e4)
 Call ID: 5573368b-c479-4d0f-b5be-97abc8c8d0e4
  Args:
    type: :Person
    source: CarlAxelArchibaldDouglas
  AddLiteral (3df5f9b6-7056-486d-a45b-ae9752196595)
 Call ID: 3df5f9b6-7056-486d-a45b-ae9752196595
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1949
    source: CarlAxelArchibaldDouglas
  AddTriple (e0096013-0383-4b5c-b05f-50dc6fe4de0d)
 Call ID: e0096013-0383-4b5c-b05f-50dc6fe4de0d
  Args:
    source: WalburgaDouglas
    target: CarlAxelArchibaldDouglas
    relation: :hasRelation
  AddLiteral (e4e07374-35e0-4816-986c-e8ea6461a75d)
 Call ID: e4e07374-35e0-4816-986c-e8ea6461a75d
  Args:
    source: WalburgaDouglas
    literal_value: 1992
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AssignClass (05f14df9-5b58-4bc3-81d0-c03849cae65d)
 Call ID: 05f14df9-5b58-4bc3-81d0-c03849cae65d
  Args:
    type: :Man
    source: ArchibaldDouglas
  AssignClass (7c66af20-fba9-43a3-8707-b6a22014a908)
 Call ID: 7c66af20-fba9-43a3-8707-b6a22014a908
  Args:
    type: :Person
    source: ArchibaldDouglas
  AssignClass (4139a07a-9949-484b-af20-e728e8ebfa8f)
 Call ID: 4139a07a-9949-484b-af20-e728e8ebfa8f
  Args:
    source: ArchibaldDouglas
    type: :Ancestor
  AssignClass (1a59328b-b1a9-4459-9e3e-9984b712b075)
 Call ID: 1a59328b-b1a9-4459-9e3e-9984b712b075
  Args:
    source: MargaretaLagerfelt
    type: :Woman
  AssignClass (788e0e05-d81c-45bc-b06b-3704f52b4604)
 Call ID: 788e0e05-d81c-45bc-b06b-3704f52b4604
  Args:
    type: :Person
    source: MargaretaLagerfelt
  AssignClass (c69db912-58c4-436b-beca-4dcf6ed46311)
 Call ID: c69db912-58c4-436b-beca-4dcf6ed46311
  Args:
    type: :Ancestor
    source: MargaretaLagerfelt
  AddTriple (e21d34a4-3570-4fa2-832d-c46f3727b063)
 Call ID: e21d34a4-3570-4fa2-832d-c46f3727b063
  Args:
    relation: :hasFather
    target: ArchibaldDouglas
    source: CarlAxelArchibaldDouglas
  AddTriple (3cd1f369-d631-4246-9997-0bfa9896418a)
 Call ID: 3cd1f369-d631-4246-9997-0bfa9896418a
  Args:
    relation: :hasMother
    target: MargaretaLagerfelt
    source: CarlAxelArchibaldDouglas
  AssignClass (5938a37e-8057-4c01-8a83-804845d2588d)
 Call ID: 5938a37e-8057-4c01-8a83-804845d2588d
  Args:
    type: :Man
    source: MauritzOttoWenzelDouglas
  AssignClass (eb5b4b7c-df1d-40d7-b517-ffaa66d4f204)
 Call ID: eb5b4b7c-df1d-40d7-b517-ffaa66d4f204
  Args:
    type: :Person
    source: MauritzOttoWenzelDouglas
  AddLiteral (9fbd7ee6-1ddf-4bdc-8190-0004e33bcde5)
 Call ID: 9fbd7ee6-1ddf-4bdc-8190-0004e33bcde5
  Args:
    literal_value: 1994
    source: MauritzOttoWenzelDouglas
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddTriple (22be8458-92e1-4995-8dd7-f2ecc60e0e79)
 Call ID: 22be8458-92e1-4995-8dd7-f2ecc60e0e79
  Args:
    target: CarlAxelArchibaldDouglas
    relation: :hasFather
    source: MauritzOttoWenzelDouglas
  AddTriple (9ca4a7cf-532c-4022-a2b7-c63584e1e379)
 Call ID: 9ca4a7cf-532c-4022-a2b7-c63584e1e379
  Args:
    target: WalburgaDouglas
    relation: :hasMother
    source: MauritzOttoWenzelDouglas
  Finish (27ef33b7-4e83-43ee-99d4-a290e69c669e)
 Call ID: 27ef33b7-4e83-43ee-99d4-a290e69c669e
  Args: