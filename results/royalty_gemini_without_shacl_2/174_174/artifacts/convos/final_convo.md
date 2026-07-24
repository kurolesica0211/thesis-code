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
Princess Katherine of Greece and Denmark (Greek: Αικατερίνη; 4 May 1913 – 2 October 2007), styled in the United Kingdom as Lady Katherine Brandram from 1947 until 2007, was the third daughter and youngest child of King Constantine I of Greece and Princess Sophia of Prussia.
Early life

Katherine was born on 4 May 1913 in the Royal Palace in Athens, a few weeks after her paternal grandfather, King George I of Greece, was assassinated in Thessaloniki.
Her godparents were Olga Constantinovna (the Dowager Queen of Greece, her paternal grandmother), Alexandra (the Dowager Queen of the United Kingdom, her paternal grandfather's sister and her maternal grandmother's sister-in-law), George V (the King of the United Kingdom, her mother's maternal cousin and her father's paternal cousin), Wilhelm II, German Emperor (her maternal uncle), The Greek Navy (represented by the Minister of Marine) and The Greek Army (represented by the Minister of War).
Katherine had five siblings – three brothers (George, Alexander and Paul, each of whom would become King of the Hellenes) and two sisters (Princess Helen, who married Crown Prince Carol of Romania, and Princess Irene who married Prince Aimone of Savoy, Duke of Spoleto).
They were reinstated following Alexander's death in 1920, but Constantine abdicated again in 1922.
The family moved to Villa Sparta in Florence, where Katherine took up painting.
Her second brother George became King George II in 1922, but was deposed in 1924.
Katherine was educated in England, at a boarding school at Broadstairs and then North Foreland Lodge.
She and the future Elizabeth II were bridesmaids at the wedding of her first cousin, Princess Marina, to Prince George in 1934.
Return to Greece and marriage

Her brother George was reinstated as king in 1935, and Katherine returned to Greece with her sister, Irene.
In 1941, after Greece had been overrun by Axis forces, she fled to South Africa with her third brother, Paul, in a Sunderland flying boat, where she worked as a nurse at a hospital in Cape Town.
On 1 April at the Royal Palace, three weeks prior to the wedding, her brother King George had a stroke and died shortly after in Katherine's presence.
George was succeeded on the Greek throne by Katherine's third brother Paul, who acted as best man at the wedding, which took place according to schedule on 21 April 1947.
On 25 August 1947, King George VI granted her the rank and title of a duke's daughter and she became known as Lady Katherine Brandram.
According to her obituary in The Daily Telegraph, "Lady Katherine lived quietly but remained in close touch with her own and the British royal families.
She attended the Queen's wedding to Prince Philip (her first cousin on her father’s side and second cousin once removed on her mother’s side), and was a guest at the service to mark Prince Philip's 80th birthday at St George's Chapel, Windsor, in 2001.
"


After the death of Infanta Beatriz of Spain in 2002, Katherine was the last surviving great-granddaughter of Queen Victoria, as well the last surviving grandchild of Frederick III, German Emperor and Victoria, Princess Royal.
Count Carl Johan Bernadotte of Sweden (31 October 1916 – 5 May 2012) as Queen Victoria's last living great-grandchild.
From the time of the death of her eldest sister Queen Helen, Queen Mother of Romania in 1982, to the time of her own death, she was Queen Victoria's most senior female line descendant.
Her death marked the end of all female-line direct descendants of Frederick III, German Emperor and Victoria, Princess Royal.
Issue

Princess Katherine of Greece and Denmark and Major Richard Campbell Andrew Brandram had one child, a son:


Bibliography

Ancestry

References

External links

@media screen{html.skin-theme-clientpref-night .mw-parser-output .sister-inline-image img{filter:invert(1)brightness(55%)contrast(250%)hue-rotate(180deg)}}@media screen and (prefers-color-scheme:dark){html.skin-theme-clientpref-os .mw-parser-output .sister-inline-image img{filter:invert(1)brightness(55%)contrast(250%)hue-rotate(180deg)}} Media related to Princess Katherine of Greece and Denmark at Wikimedia Commons



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
  AssignClass (e75647dc-da1b-4f9a-bfe3-1f2f1fc369d4)
 Call ID: e75647dc-da1b-4f9a-bfe3-1f2f1fc369d4
  Args:
    type: :Woman
    source: Princess_Katherine_of_Greece_and_Denmark
  AssignClass (6b28f49c-29a1-43a3-bd95-7f7b4c60de1b)
 Call ID: 6b28f49c-29a1-43a3-bd95-7f7b4c60de1b
  Args:
    type: :Person
    source: Princess_Katherine_of_Greece_and_Denmark
  AddLiteral (2af29f01-6907-4606-bfd8-8592704f7e67)
 Call ID: 2af29f01-6907-4606-bfd8-8592704f7e67
  Args:
    source: Princess_Katherine_of_Greece_and_Denmark
    literal_type: xsd:integer
    literal_value: 1913
    relation: :hasBirthYear
  AddLiteral (0f2d400b-7c9d-4de6-93f9-06aff7b5100e)
 Call ID: 0f2d400b-7c9d-4de6-93f9-06aff7b5100e
  Args:
    relation: :hasDeathYear
    literal_value: 2007
    source: Princess_Katherine_of_Greece_and_Denmark
    literal_type: xsd:integer
  AssignClass (05a01fcf-44f9-4ed4-93b0-b17e1a88657e)
 Call ID: 05a01fcf-44f9-4ed4-93b0-b17e1a88657e
  Args:
    source: King_Constantine_I_of_Greece
    type: :Man
  AssignClass (990ec80d-f444-43ed-8975-593d2710a893)
 Call ID: 990ec80d-f444-43ed-8975-593d2710a893
  Args:
    source: King_Constantine_I_of_Greece
    type: :Person
  AssignClass (f13459a5-cba3-4f21-96ab-d7708147e1ef)
 Call ID: f13459a5-cba3-4f21-96ab-d7708147e1ef
  Args:
    type: :Woman
    source: Princess_Sophia_of_Prussia
  AssignClass (1004779a-1c7b-4244-a2fb-c3fdc5ea32e3)
 Call ID: 1004779a-1c7b-4244-a2fb-c3fdc5ea32e3
  Args:
    type: :Person
    source: Princess_Sophia_of_Prussia
  AddTriple (3a8eaea6-7d4a-46d6-9a69-c6db88a518e2)
 Call ID: 3a8eaea6-7d4a-46d6-9a69-c6db88a518e2
  Args:
    source: Princess_Katherine_of_Greece_and_Denmark
    target: King_Constantine_I_of_Greece
    relation: :hasFather
  AddTriple (34cbad82-ce5a-4ce6-b911-ff91b148429d)
 Call ID: 34cbad82-ce5a-4ce6-b911-ff91b148429d
  Args:
    target: Princess_Sophia_of_Prussia
    relation: :hasMother
    source: Princess_Katherine_of_Greece_and_Denmark
  AssignClass (caef5a23-8eea-480a-83de-ec8f8954cf19)
 Call ID: caef5a23-8eea-480a-83de-ec8f8954cf19
  Args:
    type: :Man
    source: King_George_I_of_Greece
  AssignClass (259fce2e-6b00-4a72-aa55-462c29c8bd3a)
 Call ID: 259fce2e-6b00-4a72-aa55-462c29c8bd3a
  Args:
    source: King_George_I_of_Greece
    type: :Person
  AddTriple (ffb6f558-3e02-46fb-9af9-628baa3536f2)
 Call ID: ffb6f558-3e02-46fb-9af9-628baa3536f2
  Args:
    relation: :hasFather
    target: King_George_I_of_Greece
    source: King_Constantine_I_of_Greece
  AssignClass (cc8de2ce-8fa5-4f51-bb3b-c4497b017f9b)
 Call ID: cc8de2ce-8fa5-4f51-bb3b-c4497b017f9b
  Args:
    source: George_II_of_Greece
    type: :Man
  AssignClass (5ad640bc-d217-43bb-8b7e-8d8558acab70)
 Call ID: 5ad640bc-d217-43bb-8b7e-8d8558acab70
  Args:
    source: George_II_of_Greece
    type: :Person
  AssignClass (5d2e2fed-a150-4c58-9115-5ec2639ba720)
 Call ID: 5d2e2fed-a150-4c58-9115-5ec2639ba720
  Args:
    type: :Man
    source: Alexander_of_Greece
  AssignClass (64363d40-bff4-44ca-a23b-527fce20332c)
 Call ID: 64363d40-bff4-44ca-a23b-527fce20332c
  Args:
    type: :Person
    source: Alexander_of_Greece
  AssignClass (1e1a7333-4d99-4970-8d71-c58eb8f7faf6)
 Call ID: 1e1a7333-4d99-4970-8d71-c58eb8f7faf6
  Args:
    source: Paul_of_Greece
    type: :Man
  AssignClass (781a0236-a9ef-413c-9b60-28ef8c4e50d1)
 Call ID: 781a0236-a9ef-413c-9b60-28ef8c4e50d1
  Args:
    source: Paul_of_Greece
    type: :Person
  AssignClass (e9739244-4474-4ad2-b77b-a980291d186f)
 Call ID: e9739244-4474-4ad2-b77b-a980291d186f
  Args:
    type: :Woman
    source: Princess_Helen_of_Greece
  AssignClass (e30b2af1-e008-4a0d-a65a-1fa57fd5b326)
 Call ID: e30b2af1-e008-4a0d-a65a-1fa57fd5b326
  Args:
    source: Princess_Helen_of_Greece
    type: :Person
  AssignClass (0891982c-fc0b-471f-89c5-1423ba721d5a)
 Call ID: 0891982c-fc0b-471f-89c5-1423ba721d5a
  Args:
    source: Princess_Irene_of_Greece
    type: :Woman
  AssignClass (7c3c8098-69ad-4187-ab4d-edd3630bd282)
 Call ID: 7c3c8098-69ad-4187-ab4d-edd3630bd282
  Args:
    type: :Person
    source: Princess_Irene_of_Greece
  AddTriple (7c72704d-644f-4177-aa7b-9ef6c0922de1)
 Call ID: 7c72704d-644f-4177-aa7b-9ef6c0922de1
  Args:
    source: Princess_Katherine_of_Greece_and_Denmark
    target: George_II_of_Greece
    relation: :hasBrother
  AddTriple (d5fb849b-93a8-4873-b144-b026c4f9c645)
 Call ID: d5fb849b-93a8-4873-b144-b026c4f9c645
  Args:
    target: Alexander_of_Greece
    relation: :hasBrother
    source: Princess_Katherine_of_Greece_and_Denmark
  AddTriple (932153c9-742b-4464-b632-0350d98b2bac)
 Call ID: 932153c9-742b-4464-b632-0350d98b2bac
  Args:
    source: Princess_Katherine_of_Greece_and_Denmark
    relation: :hasBrother
    target: Paul_of_Greece
  AddTriple (60586a07-bb6b-4194-b728-0bb726378b3a)
 Call ID: 60586a07-bb6b-4194-b728-0bb726378b3a
  Args:
    source: Princess_Katherine_of_Greece_and_Denmark
    target: Princess_Helen_of_Greece
    relation: :hasSister
  AddTriple (b0069ec6-a070-444b-881a-1198c1d01205)
 Call ID: b0069ec6-a070-444b-881a-1198c1d01205
  Args:
    source: Princess_Katherine_of_Greece_and_Denmark
    relation: :hasSister
    target: Princess_Irene_of_Greece
  AssignClass (6b3cd5bc-be05-46fc-9232-148d39025d10)
 Call ID: 6b3cd5bc-be05-46fc-9232-148d39025d10
  Args:
    type: :Man
    source: Major_Richard_Campbell_Andrew_Brandram
  AssignClass (4431cd84-da5f-4a6c-aa7f-805fd7eb8c94)
 Call ID: 4431cd84-da5f-4a6c-aa7f-805fd7eb8c94
  Args:
    source: Major_Richard_Campbell_Andrew_Brandram
    type: :Person
  AddTriple (b979ce0f-f546-4bb3-9073-d6a1d89fc31f)
 Call ID: b979ce0f-f546-4bb3-9073-d6a1d89fc31f
  Args:
    source: Princess_Katherine_of_Greece_and_Denmark
    relation: :hasRelation
    target: Major_Richard_Campbell_Andrew_Brandram
  AddLiteral (b8be9d5d-644e-47b3-8897-8d6e1dfbadc1)
 Call ID: b8be9d5d-644e-47b3-8897-8d6e1dfbadc1
  Args:
    source: Princess_Katherine_of_Greece_and_Denmark
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1947
  AddLiteral (c4990436-6046-4a22-8b2c-a6dd3590d023)
 Call ID: c4990436-6046-4a22-8b2c-a6dd3590d023
  Args:
    source: Princess_Katherine_of_Greece_and_Denmark
    literal_type: xsd:string
    literal_value: Lady Katherine Brandram
    relation: :knownAs
  Finish (250cda81-8dcd-4b69-b3a4-e13717fecdd8)
 Call ID: 250cda81-8dcd-4b69-b3a4-e13717fecdd8
  Args: