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
  AssignClass (34beda66-d355-47d7-ac64-2eb3e95f9749)
 Call ID: 34beda66-d355-47d7-ac64-2eb3e95f9749
  Args:
    type: :Man
    source: William_Prince_of_Orange
  AssignClass (2241fca3-b60b-415c-8f0f-31cf34d74c9c)
 Call ID: 2241fca3-b60b-415c-8f0f-31cf34d74c9c
  Args:
    type: :Person
    source: William_Prince_of_Orange
  AddLiteral (1e03efe9-cb32-4999-8814-313a1bfae320)
 Call ID: 1e03efe9-cb32-4999-8814-313a1bfae320
  Args:
    source: William_Prince_of_Orange
    literal_type: xsd:integer
    literal_value: 1840
    relation: :hasBirthYear
  AddLiteral (fbb61229-88e5-4210-92d8-528d9296adc8)
 Call ID: fbb61229-88e5-4210-92d8-528d9296adc8
  Args:
    literal_value: 1879
    literal_type: xsd:integer
    source: William_Prince_of_Orange
    relation: :hasDeathYear
  AddLiteral (db7a8dd6-9543-4a97-8afd-d8cb5d461c30)
 Call ID: db7a8dd6-9543-4a97-8afd-d8cb5d461c30
  Args:
    relation: :alsoKnownAs
    literal_value: Prince Lemon
    source: William_Prince_of_Orange
    literal_type: xsd:string
  AssignClass (f6f071db-e1f5-4ac4-afc7-a3a465fe32a5)
 Call ID: f6f071db-e1f5-4ac4-afc7-a3a465fe32a5
  Args:
    type: :Man
    source: King_William_III
  AssignClass (fe92ee6d-096d-44f7-a6b3-26d8c9908d03)
 Call ID: fe92ee6d-096d-44f7-a6b3-26d8c9908d03
  Args:
    type: :Person
    source: King_William_III
  AddTriple (7f5ea3ee-ec46-41eb-8b49-a0fc82babe61)
 Call ID: 7f5ea3ee-ec46-41eb-8b49-a0fc82babe61
  Args:
    relation: :hasFather
    source: William_Prince_of_Orange
    target: King_William_III
  AssignClass (74a95827-fa45-4ed5-bb51-410fe4db3d1e)
 Call ID: 74a95827-fa45-4ed5-bb51-410fe4db3d1e
  Args:
    type: :Woman
    source: Princess_Sophie_of_Wurttemberg
  AssignClass (3726881b-d00f-4572-a2e3-e1a1cc4f5142)
 Call ID: 3726881b-d00f-4572-a2e3-e1a1cc4f5142
  Args:
    type: :Person
    source: Princess_Sophie_of_Wurttemberg
  AddTriple (2a7043bf-5f62-4b06-84c1-1eabd8742653)
 Call ID: 2a7043bf-5f62-4b06-84c1-1eabd8742653
  Args:
    target: Princess_Sophie_of_Wurttemberg
    source: William_Prince_of_Orange
    relation: :hasMother
  AssignClass (495e2e9d-6fa7-4c89-9bc7-18517efb73e7)
 Call ID: 495e2e9d-6fa7-4c89-9bc7-18517efb73e7
  Args:
    type: :Man
    source: King_William_I
  AssignClass (5aaac18c-f3fa-4d94-b122-348073a51720)
 Call ID: 5aaac18c-f3fa-4d94-b122-348073a51720
  Args:
    type: :Person
    source: King_William_I
  AddTriple (efa89fb6-742d-4349-8f5a-5c60515a365a)
 Call ID: efa89fb6-742d-4349-8f5a-5c60515a365a
  Args:
    source: William_Prince_of_Orange
    target: King_William_I
    relation: :hasAncestor
  AssignClass (ccf59c0b-9232-4ff3-83f6-f5c42f03d736)
 Call ID: ccf59c0b-9232-4ff3-83f6-f5c42f03d736
  Args:
    type: :Man
    source: King_William_II
  AssignClass (3ea69736-4f2f-46e2-a63d-d3ab143d962a)
 Call ID: 3ea69736-4f2f-46e2-a63d-d3ab143d962a
  Args:
    type: :Person
    source: King_William_II
  AddTriple (9c7c9bad-5d3f-4e11-8830-6577545046e8)
 Call ID: 9c7c9bad-5d3f-4e11-8830-6577545046e8
  Args:
    target: King_William_II
    source: William_Prince_of_Orange
    relation: :hasAncestor
  AssignClass (3fd7dab8-18f7-45e2-865b-c1065b1c1b67)
 Call ID: 3fd7dab8-18f7-45e2-865b-c1065b1c1b67
  Args:
    type: :Man
    source: Alexander
  AssignClass (b2b0cff5-d778-4eb6-8984-128462cdde4f)
 Call ID: b2b0cff5-d778-4eb6-8984-128462cdde4f
  Args:
    type: :Person
    source: Alexander
  AddTriple (3d798c83-e429-4f55-a1af-fca5176dd9b3)
 Call ID: 3d798c83-e429-4f55-a1af-fca5176dd9b3
  Args:
    relation: :hasBrother
    target: Alexander
    source: William_Prince_of_Orange
  AssignClass (55253524-76e4-4a0c-840b-f90ac8615822)
 Call ID: 55253524-76e4-4a0c-840b-f90ac8615822
  Args:
    type: :Woman
    source: Wilhelmina
  AssignClass (91d04b0b-6b09-4a6b-b72f-1a1d57fd67a5)
 Call ID: 91d04b0b-6b09-4a6b-b72f-1a1d57fd67a5
  Args:
    type: :Person
    source: Wilhelmina
  AddTriple (d62a9c7e-efef-4d23-a87b-e1e0a51d98d9)
 Call ID: d62a9c7e-efef-4d23-a87b-e1e0a51d98d9
  Args:
    relation: :hasSister
    target: Wilhelmina
    source: William_Prince_of_Orange
  AssignClass (0b4d2857-d84c-40f9-9b21-17e7f0650462)
 Call ID: 0b4d2857-d84c-40f9-9b21-17e7f0650462
  Args:
    type: :Woman
    source: Princess_Augusta_of_Great_Britain
  AssignClass (97d43d0d-6c28-40a8-bff9-035d17ff2a39)
 Call ID: 97d43d0d-6c28-40a8-bff9-035d17ff2a39
  Args:
    type: :Person
    source: Princess_Augusta_of_Great_Britain
  AddTriple (e5315f2b-bfab-412f-b005-29fbcbf7581d)
 Call ID: e5315f2b-bfab-412f-b005-29fbcbf7581d
  Args:
    relation: :hasAncestor
    target: Princess_Augusta_of_Great_Britain
    source: William_Prince_of_Orange
  Finish (85bb6790-f2fe-4a83-b0ab-bcbf2221a756)
 Call ID: 85bb6790-f2fe-4a83-b0ab-bcbf2221a756
  Args: