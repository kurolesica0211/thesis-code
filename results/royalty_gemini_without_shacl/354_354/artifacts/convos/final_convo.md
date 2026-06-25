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
William, Prince of Orange (Willem Nicolaas Alexander Frederik Karel Hendrik; 4 September 1840 – 11 June 1879), was heir apparent to the Dutch throne as the eldest son of King William III from 17 March 1849 until his death.
Early life

Prince William was the eldest son of King William III of the Netherlands and his first wife, Princess Sophie of Württemberg.
He was also seventeenth in the line of succession to the British throne, his claim being through his mother Sophie's great-grandmother Princess Augusta of Great Britain.
On 7 October 1840, only a month after his birth, his great-grandfather, the reigning King William I of the Netherlands, abdicated the throne due to disappointment over the recent Treaty of London, which recognized the independence of Belgium (previously provinces of the United Kingdom of the Netherlands), and the intention of marrying a Roman Catholic and Belgian noblewoman, Henrietta d'Oultremont.
In 1849, after the death of his grandfather King William II of the Netherlands, he became Prince of Orange as heir apparent.
Failed marriage attempts

After attempts to marry Prince William off to Princess Alice of the United Kingdom, the second daughter of Queen Victoria or Grand Duchess Maria Alexandrovna of Russia failed, the prince fell in love with the 19-year-old Countess Mathilde van Limburg-Stirum in 1873.
The relationship between the prince and his parents became very problematic, as his parents (who rarely agreed on anything) refused William's wish to accept Mathilde as his bride in 1874.
Also a rumour circulated that Mathilde was an illegitimate daughter of King William III and so William would potentially be marrying his own half-sister.
The 33-year-old William wanted to marry, if necessary, without the consent of his parents (this would have cost him his position in the line of succession).
Since they denied permission, the prince's attempt to marry Mathilde failed.
Death and aftermath

Heavily disillusioned with his situation in the Netherlands, Prince William then went into exile in Paris, where he threw himself into a life of sex, drinking and gambling.
The Duke de Gramont-Caderousse, a French fellow hedonist, gave him the nickname "Prince Lemon" ; the nickname became popular among the regulars in the recently created boulevards and the Parisian newspapers when they reported about his debauched lifestyle.
Prince William died at the age of 38 in his apartment in the Rue Auber, near the Paris Opera from a combination of typhus, liver complaints and total exhaustion.
After his death, his brother Alexander became heir-apparent and Prince of Orange.
His half-sister, the future queen Wilhelmina, was born a year after his death.
Honours

Ancestry

Footnotes

2 gave up the title "Prince of the Netherlands, but still held the title "Prince of Orange-Nassau"
3 title granted by Royal Decree to descendants of Princess Irene



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
  AssignClass (2b29728f-4c27-4a5d-b884-8dbfccdd5327)
 Call ID: 2b29728f-4c27-4a5d-b884-8dbfccdd5327
  Args:
    type: :Man
    source: William_Prince_of_Orange
  AssignClass (f4e21381-5d16-4f69-a31e-ff8a37ad3c02)
 Call ID: f4e21381-5d16-4f69-a31e-ff8a37ad3c02
  Args:
    type: :Person
    source: William_Prince_of_Orange
  AddLiteral (3b797a24-1ce5-4921-bd0e-4b90dd70a5ea)
 Call ID: 3b797a24-1ce5-4921-bd0e-4b90dd70a5ea
  Args:
    source: William_Prince_of_Orange
    literal_value: 1840
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (17686895-eff2-4b4f-ac63-378e59d4caf9)
 Call ID: 17686895-eff2-4b4f-ac63-378e59d4caf9
  Args:
    literal_value: 1879
    source: William_Prince_of_Orange
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (776db9dc-65d6-440d-941a-f24770f79eaf)
 Call ID: 776db9dc-65d6-440d-941a-f24770f79eaf
  Args:
    type: :Man
    source: King_William_III
  AssignClass (048e5cb9-7f6a-4208-b79a-74946c07833e)
 Call ID: 048e5cb9-7f6a-4208-b79a-74946c07833e
  Args:
    source: King_William_III
    type: :Person
  AssignClass (85377b42-f0af-413d-af4e-76731d0f75b4)
 Call ID: 85377b42-f0af-413d-af4e-76731d0f75b4
  Args:
    type: :Woman
    source: Princess_Sophie_of_Wurttemberg
  AssignClass (d03e9a5b-52f5-42bd-8eb6-7eac02dae26e)
 Call ID: d03e9a5b-52f5-42bd-8eb6-7eac02dae26e
  Args:
    source: Princess_Sophie_of_Wurttemberg
    type: :Person
  AddTriple (43c6db83-3208-46c9-b80a-d04efca1a487)
 Call ID: 43c6db83-3208-46c9-b80a-d04efca1a487
  Args:
    relation: :hasFather
    source: William_Prince_of_Orange
    target: King_William_III
  AddTriple (a1bcd123-4b14-4d20-ac40-2a5db1245d42)
 Call ID: a1bcd123-4b14-4d20-ac40-2a5db1245d42
  Args:
    source: William_Prince_of_Orange
    target: Princess_Sophie_of_Wurttemberg
    relation: :hasMother
  AssignClass (98f2ed3b-0e94-4c9f-9c1d-ad46a4412acf)
 Call ID: 98f2ed3b-0e94-4c9f-9c1d-ad46a4412acf
  Args:
    type: :Man
    source: King_William_I
  AssignClass (2ce60bca-92de-4427-8e16-31e884adb4f5)
 Call ID: 2ce60bca-92de-4427-8e16-31e884adb4f5
  Args:
    type: :Person
    source: King_William_I
  AddTriple (e4b573cc-c309-4f53-9cdf-b90096abf968)
 Call ID: e4b573cc-c309-4f53-9cdf-b90096abf968
  Args:
    relation: :hasFather
    source: King_William_III
    target: King_William_II
  AssignClass (d1152b4b-9395-4e36-858f-2bac0a4c0a97)
 Call ID: d1152b4b-9395-4e36-858f-2bac0a4c0a97
  Args:
    source: King_William_II
    type: :Man
  AssignClass (8f41ddba-67e0-43ac-b29c-50286619d936)
 Call ID: 8f41ddba-67e0-43ac-b29c-50286619d936
  Args:
    type: :Person
    source: King_William_II
  AddTriple (bd3c59e5-27fd-4349-b8f9-8e09aac06aaf)
 Call ID: bd3c59e5-27fd-4349-b8f9-8e09aac06aaf
  Args:
    target: King_William_I
    source: King_William_II
    relation: :hasFather
  AssignClass (4e4dec2b-bed1-477d-a742-2fc6838f3686)
 Call ID: 4e4dec2b-bed1-477d-a742-2fc6838f3686
  Args:
    source: Princess_Augusta_of_Great_Britain
    type: :Woman
  AssignClass (e7a642fe-89db-439f-a9c0-da993d4dbcab)
 Call ID: e7a642fe-89db-439f-a9c0-da993d4dbcab
  Args:
    type: :Person
    source: Princess_Augusta_of_Great_Britain
  AddTriple (313907c0-5617-4cc4-9770-026091af8337)
 Call ID: 313907c0-5617-4cc4-9770-026091af8337
  Args:
    source: Princess_Sophie_of_Wurttemberg
    target: Princess_Augusta_of_Great_Britain
    relation: :hasMother
  AssignClass (a65ea766-6368-4e39-8eb8-ce1db3e07a71)
 Call ID: a65ea766-6368-4e39-8eb8-ce1db3e07a71
  Args:
    source: Alexander
    type: :Man
  AssignClass (aaca4f66-8e5f-4348-8dd7-c29534a2d6b3)
 Call ID: aaca4f66-8e5f-4348-8dd7-c29534a2d6b3
  Args:
    source: Alexander
    type: :Person
  AddTriple (1b33b767-2204-4415-8bb3-5991f4d804e1)
 Call ID: 1b33b767-2204-4415-8bb3-5991f4d804e1
  Args:
    target: Alexander
    source: William_Prince_of_Orange
    relation: :hasBrother
  AddTriple (28dba144-8ada-42db-ac25-39e8ca8c05d5)
 Call ID: 28dba144-8ada-42db-ac25-39e8ca8c05d5
  Args:
    relation: :hasFather
    source: Alexander
    target: King_William_III
  AssignClass (24113232-f298-4adc-9eb7-3338fcb47c80)
 Call ID: 24113232-f298-4adc-9eb7-3338fcb47c80
  Args:
    type: :Woman
    source: Wilhelmina
  AssignClass (b797142e-4d71-449c-96ea-945d36f78102)
 Call ID: b797142e-4d71-449c-96ea-945d36f78102
  Args:
    type: :Person
    source: Wilhelmina
  AddTriple (9a76f31c-2ade-46b4-9a24-79b75c5e945e)
 Call ID: 9a76f31c-2ade-46b4-9a24-79b75c5e945e
  Args:
    target: King_William_III
    source: Wilhelmina
    relation: :hasMother
  AddTriple (02e9d5df-9148-4a2c-a361-db1fdfcc14d2)
 Call ID: 02e9d5df-9148-4a2c-a361-db1fdfcc14d2
  Args:
    target: Wilhelmina
    source: William_Prince_of_Orange
    relation: :hasSister
  AddLiteral (5694ab47-3485-47da-bd2e-f5f6c035304e)
 Call ID: 5694ab47-3485-47da-bd2e-f5f6c035304e
  Args:
    literal_type: xsd:string
    relation: :alsoKnownAs
    literal_value: Prince Lemon
    source: William_Prince_of_Orange
  Finish (3c09c8c6-ad82-4dc9-996a-17656cd0968b)
 Call ID: 3c09c8c6-ad82-4dc9-996a-17656cd0968b
  Args: