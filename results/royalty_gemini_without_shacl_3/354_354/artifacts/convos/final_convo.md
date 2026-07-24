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
  AssignClass (f7c073a2-e2e8-437f-892e-ed111b517ec7)
 Call ID: f7c073a2-e2e8-437f-892e-ed111b517ec7
  Args:
    source: William_Prince_of_Orange
    type: :Man
  AssignClass (8f80418a-e56e-4bc3-bf27-f126ab47c53e)
 Call ID: 8f80418a-e56e-4bc3-bf27-f126ab47c53e
  Args:
    type: :Person
    source: William_Prince_of_Orange
  AddLiteral (a78650ed-5036-4755-978b-cb37984d7c14)
 Call ID: a78650ed-5036-4755-978b-cb37984d7c14
  Args:
    source: William_Prince_of_Orange
    literal_value: 1840
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (f4762d3e-35e6-498b-823a-033788f1c881)
 Call ID: f4762d3e-35e6-498b-823a-033788f1c881
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1879
    source: William_Prince_of_Orange
  AddLiteral (33116a24-1b2e-49be-a794-186f3f2b0a86)
 Call ID: 33116a24-1b2e-49be-a794-186f3f2b0a86
  Args:
    source: William_Prince_of_Orange
    literal_value: Prince Lemon
    relation: :alsoKnownAs
    literal_type: xsd:string
  AssignClass (27517082-158c-40ed-bfae-76ff9d732cd9)
 Call ID: 27517082-158c-40ed-bfae-76ff9d732cd9
  Args:
    type: :Man
    source: King_William_III
  AssignClass (d0339d4c-de1a-4b0f-85bf-b82790ec4ee8)
 Call ID: d0339d4c-de1a-4b0f-85bf-b82790ec4ee8
  Args:
    source: King_William_III
    type: :Person
  AssignClass (a345e88d-3272-443a-87df-672995f9ce55)
 Call ID: a345e88d-3272-443a-87df-672995f9ce55
  Args:
    type: :Woman
    source: Princess_Sophie_of_Wurttemberg
  AssignClass (cbf83f90-640d-42b7-85cc-5b50e837e4e6)
 Call ID: cbf83f90-640d-42b7-85cc-5b50e837e4e6
  Args:
    type: :Person
    source: Princess_Sophie_of_Wurttemberg
  AddTriple (343e8b7a-fcd0-4811-b4ec-5582eaf4d52d)
 Call ID: 343e8b7a-fcd0-4811-b4ec-5582eaf4d52d
  Args:
    target: King_William_III
    source: William_Prince_of_Orange
    relation: :hasFather
  AddTriple (e80ec002-21ca-4b17-9690-e86838521012)
 Call ID: e80ec002-21ca-4b17-9690-e86838521012
  Args:
    relation: :hasMother
    source: William_Prince_of_Orange
    target: Princess_Sophie_of_Wurttemberg
  AssignClass (79c9c892-4bc5-437b-9282-83f40246ecee)
 Call ID: 79c9c892-4bc5-437b-9282-83f40246ecee
  Args:
    source: King_William_I
    type: :Man
  AssignClass (f57b88e4-e376-4ad1-9a9e-6647e021bf3e)
 Call ID: f57b88e4-e376-4ad1-9a9e-6647e021bf3e
  Args:
    source: King_William_I
    type: :Person
  AddTriple (6a105e12-d515-4ae7-ba52-0f9a1a39b594)
 Call ID: 6a105e12-d515-4ae7-ba52-0f9a1a39b594
  Args:
    relation: :hasFather
    target: King_William_II
    source: King_William_III
  AssignClass (79aa22e0-a267-4acf-9bb5-694b41dc4336)
 Call ID: 79aa22e0-a267-4acf-9bb5-694b41dc4336
  Args:
    source: King_William_II
    type: :Man
  AssignClass (da959969-25d8-4660-940d-d8fc868a60c0)
 Call ID: da959969-25d8-4660-940d-d8fc868a60c0
  Args:
    type: :Person
    source: King_William_II
  AddTriple (e9016c48-8896-4581-b8fa-752416e5b60f)
 Call ID: e9016c48-8896-4581-b8fa-752416e5b60f
  Args:
    relation: :hasFather
    target: King_William_I
    source: King_William_II
  AssignClass (8f5ef03d-eee4-4653-b16d-b80e0e02a922)
 Call ID: 8f5ef03d-eee4-4653-b16d-b80e0e02a922
  Args:
    source: Princess_Augusta_of_Great_Britain
    type: :Woman
  AssignClass (bd51a273-4701-4be3-a13e-f4fdc1a8dd12)
 Call ID: bd51a273-4701-4be3-a13e-f4fdc1a8dd12
  Args:
    source: Princess_Augusta_of_Great_Britain
    type: :Person
  AddTriple (9713d745-f2b1-4946-b564-e16293dfc697)
 Call ID: 9713d745-f2b1-4946-b564-e16293dfc697
  Args:
    source: Princess_Sophie_of_Wurttemberg
    target: Princess_Augusta_of_Great_Britain
    relation: :hasMother
  AssignClass (5c955619-3b40-409a-958a-7c0ec085b9c4)
 Call ID: 5c955619-3b40-409a-958a-7c0ec085b9c4
  Args:
    type: :Woman
    source: Countess_Mathilde_van_Limburg-Stirum
  AssignClass (414a7063-c89b-48ee-8610-a7a67ce6fc4b)
 Call ID: 414a7063-c89b-48ee-8610-a7a67ce6fc4b
  Args:
    type: :Person
    source: Countess_Mathilde_van_Limburg-Stirum
  AssignClass (45faa4e4-0c38-4a1b-b32c-c0257592674e)
 Call ID: 45faa4e4-0c38-4a1b-b32c-c0257592674e
  Args:
    source: Alexander
    type: :Man
  AssignClass (3fe0da17-31b3-4ac2-bd5e-f9a04c77eddc)
 Call ID: 3fe0da17-31b3-4ac2-bd5e-f9a04c77eddc
  Args:
    type: :Person
    source: Alexander
  AddTriple (8f24d680-84d9-4d8d-ac88-3fbab8af02dc)
 Call ID: 8f24d680-84d9-4d8d-ac88-3fbab8af02dc
  Args:
    source: Alexander
    target: King_William_III
    relation: :hasFather
  AddTriple (db9efc75-57d7-45ed-a71a-74b00db2b5b5)
 Call ID: db9efc75-57d7-45ed-a71a-74b00db2b5b5
  Args:
    source: Alexander
    target: Princess_Sophie_of_Wurttemberg
    relation: :hasMother
  AssignClass (4c5634e7-70ca-48f9-befe-3984e4e9fdca)
 Call ID: 4c5634e7-70ca-48f9-befe-3984e4e9fdca
  Args:
    type: :Woman
    source: Wilhelmina
  AssignClass (fffe8e4e-c8da-4952-943d-fe4c86d21557)
 Call ID: fffe8e4e-c8da-4952-943d-fe4c86d21557
  Args:
    source: Wilhelmina
    type: :Person
  AddTriple (e59670b6-af4e-4bf0-a47a-99e314d314d7)
 Call ID: e59670b6-af4e-4bf0-a47a-99e314d314d7
  Args:
    source: Wilhelmina
    target: King_William_III
    relation: :hasFather
  Finish (846a3d75-5c9b-4dad-bfc2-f1caca382736)
 Call ID: 846a3d75-5c9b-4dad-bfc2-f1caca382736
  Args: