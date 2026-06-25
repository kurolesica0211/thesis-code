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
Ernest Augustus (Ernest Augustus Christian George; German: Ernst August Christian Georg; 17 November 1887 – 30 January 1953) was Duke of Brunswick from 2 November 1913 to 8 November 1918.
He was also a maternal grandson of Christian IX of Denmark and the son-in-law of German Emperor Wilhelm II.
Early life

Ernest Augustus was born at Penzing near Vienna, the sixth and youngest child of former Crown Prince Ernest Augustus of Hanover and his wife, Princess Thyra of Denmark.
His great-grandfather, Prince Ernest Augustus, Duke of Cumberland, the fifth son of George III of the United Kingdom, became king of Hanover in 1837 because Salic Law barred Victoria, Queen of the United Kingdom, from inheriting the Hanoverian throne.
His father succeeded as pretender to the Hanoverian throne and as Duke of Cumberland and Teviotdale in the peerage of Great Britain in 1878.
The younger Ernest Augustus became heir apparent to the dukedom of Cumberland and to the Hanoverian claim upon the deaths of his two elder brothers, George and Christian.
In 1884, his paternal great-granduncle the reigning Duke of Brunswick (a male line descendant of Henry, the older brother of William, his male line ancestor) died.
Since the younger branch of the House of Welf ended with him, under house rules it would have passed to the Duke of Cumberland, who immediately claimed the throne.
However, the Imperial Chancellor, Otto von Bismarck, managed to get the Federal Council (Bundesrat) of the German Empire to rule that the Duke of Cumberland would disturb the peace of the empire if he ascended the throne of Brunswick.
Bismarck did this because the duke had never formally renounced his claims to the kingdom of Hanover, which had been annexed to Prussia in 1866 following the end of the Austro-Prussian War (Hanover had sided with losing Austria).
Instead, Prince Albrecht of Prussia became the regent of Brunswick.
After Prince Albrecht's death in 1906, the duke offered that he and his elder son, Prince George, would renounce their claims to the Duchy of Brunswick in order to allow Ernest Augustus, his only other surviving son, to take possession of the Duchy, but this option was rejected by the Bundesrat and the regency continued, this time under Duke Johann Albrecht of Mecklenburg-Schwerin, who had previously acted as regent for his nephew in Mecklenburg.
Marriage and accession to the duchy of Brunswick

When Ernest Augustus's older brother George died in an automobile accident on 20 May 1912, the German Emperor, Wilhelm II, sent a message of condolence to the Duke of Cumberland.
In response to this friendly gesture, the Duke sent his only surviving son, Ernest Augustus, to Berlin to thank the Emperor for his message.
Ernest Augustus and Wilhelm II were third cousins through George III of the United Kingdom.
In Berlin, Ernest Augustus met and fell in love with the emperor's only daughter, Princess Victoria Louise of Prussia.
On 24 May 1913, Ernest Augustus and Victoria Louise, third cousins once removed through descent from George III's sons King Ernest Augustus of Hanover and Edward, Duke of Kent, were married to each other.
This marriage ended the decades-long rift between the Houses of Hohenzollern and Hanover.
The wedding of Prince Ernest Augustus and Princess Victoria Louise was also the last great gathering of European sovereigns before the outbreak of the Great War, as recalled by Constantine II of Greece, a grandson of the married couple, in 2003.
In addition to the German Emperor and Empress and the Duke and Duchess of Cumberland, King George V and Queen Mary of the United Kingdom and Tsar Nicholas II attended.
Upon the announcement of his betrothal to Princess Victoria Louise in February 1913, Ernest Augustus swore allegiance to the German Empire and accepted a commission as a cavalry captain and company commander in the Zieten–Hussars, a Prussian Army regiment in which his grandfather (George V) and great-grandfather (Ernest Augustus) had been colonels.
On 27 October 1913, the Duke of Cumberland formally renounced his claims to the duchy of Brunswick in favor of his surviving son.
The following day, the Federal Council voted to allow Ernest Augustus to become the reigning Duke of Brunswick.
The new Duke of Brunswick formally took possession of his duchy on 1 November.
The new duke and duchess of Brunswick moved into Brunswick Palace in the capital of Brunswick and began their family with the birth of their eldest son, Prince Ernest Augustus, less than a year after their wedding.
During the First World War, Ernest Augustus rose to the rank of major-general.
Abdication and later life

In 1917, the British dukedom of Ernest Augustus's father, and his own title as a Prince of the United Kingdom of Great Britain and Ireland, were removed by the Titles Deprivation Act 1917, which took effect in 1919, as a result of the Duke's service in the German army during the war.
On 8 November 1918, Ernest Augustus was forced to abdicate his throne, as were all the other German kings, grand dukes, dukes, and princes during the German Revolution of 1918–1919.
Thus, when his father died in 1923, Ernest Augustus did not succeed to his father's title of Duke of Cumberland.
For the next thirty years, Ernest Augustus remained as head of the House of Hanover, living in retirement on his various estates, mainly Blankenburg Castle in Germany and Cumberland Castle in Gmunden, Austria.
He also owned Marienburg Castle near Hanover, although rarely ever living there until 1945.
While Ernest Augustus never officially joined the Nazi Party, he donated funds and was close to several leaders.
As a former British prince, Ernest Augustus, as well as Victoria Louise, desired a rapprochement between the United Kingdom and Germany.
Ostensibly desiring to pursue an alliance with the UK, in the mid-1930s, Adolf Hitler took advantage of their sentiment by asking the couple to arrange a match between their daughter Princess Frederica and the Prince of Wales.
The Duke and Duchess of Brunswick refused, believing that the age difference was too great.
In 1938 Princess Frederica married Prince Paul of Greece, brother and heir-presumptive of King George II of Greece.
Ernest Augustus lived to see his daughter Frederica become a queen consort in 1947 when her husband Paul became King of the Hellenes.
Ernest Augustus died at Marienburg Castle in 1953.
He was interred, later to be joined by the remains of his wife, in front of the Royal Mausoleum in the Berggarten at Herrenhausen Gardens in Hanover, which is the burial chapel of King Ernest Augustus of Hanover and his wife.
Issue

The Duke and Duchess of Brunswick had five children:


Honours

Ancestry

References

Sources

External links



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
  AssignClass (d1eaab80-a450-4fe7-833e-4701c25c47a5)
 Call ID: d1eaab80-a450-4fe7-833e-4701c25c47a5
  Args:
    type: :Man
    source: ErnestAugustus
  AddLiteral (0fec4b00-5690-49c3-b082-e157afeb08b1)
 Call ID: 0fec4b00-5690-49c3-b082-e157afeb08b1
  Args:
    source: ErnestAugustus
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1887
  AddLiteral (3f9e0cb4-e72b-4ea0-8b23-30f3d573c2fc)
 Call ID: 3f9e0cb4-e72b-4ea0-8b23-30f3d573c2fc
  Args:
    source: ErnestAugustus
    relation: :hasDeathYear
    literal_value: 1953
    literal_type: xsd:integer
  AssignClass (199fd9fe-74e0-47b1-b5e8-adcc5721fef3)
 Call ID: 199fd9fe-74e0-47b1-b5e8-adcc5721fef3
  Args:
    source: ErnestAugustusOfHanover
    type: :Man
  AssignClass (732ac6a9-02d8-46f2-84c8-9c96e618c662)
 Call ID: 732ac6a9-02d8-46f2-84c8-9c96e618c662
  Args:
    source: PrincessThyra
    type: :Woman
  AddTriple (b6d8c3d2-7997-475c-93fe-9cb60879d493)
 Call ID: b6d8c3d2-7997-475c-93fe-9cb60879d493
  Args:
    source: ErnestAugustus
    target: ErnestAugustusOfHanover
    relation: :hasFather
  AddTriple (89935071-adb2-4695-b4a4-7f4076901918)
 Call ID: 89935071-adb2-4695-b4a4-7f4076901918
  Args:
    target: PrincessThyra
    source: ErnestAugustus
    relation: :hasMother
  AssignClass (da8d4315-f9ce-4c18-b282-35e40fbf83dc)
 Call ID: da8d4315-f9ce-4c18-b282-35e40fbf83dc
  Args:
    type: :Man
    source: George
  AssignClass (ff662f16-f149-48d4-a48c-06f6fa99a8c1)
 Call ID: ff662f16-f149-48d4-a48c-06f6fa99a8c1
  Args:
    source: Christian
    type: :Man
  AddTriple (19bd6df7-2b22-49f7-ba02-f76f1d7d81d3)
 Call ID: 19bd6df7-2b22-49f7-ba02-f76f1d7d81d3
  Args:
    relation: :isBrotherOf
    source: ErnestAugustus
    target: George
  AddTriple (12963704-7e4d-4fcb-9b35-1a409095baef)
 Call ID: 12963704-7e4d-4fcb-9b35-1a409095baef
  Args:
    source: ErnestAugustus
    target: Christian
    relation: :isBrotherOf
  AssignClass (f40d3655-582f-466e-8a8e-0ebaf8b0ecd6)
 Call ID: f40d3655-582f-466e-8a8e-0ebaf8b0ecd6
  Args:
    source: VictoriaLouise
    type: :Woman
  AddTriple (42958dea-a1cc-4792-87f2-bb898bec41ef)
 Call ID: 42958dea-a1cc-4792-87f2-bb898bec41ef
  Args:
    relation: :hasMother
    target: PrincessThyra
    source: ErnestAugustus
  AddTriple (12d67756-0618-45d2-bc88-1a6c8d624088)
 Call ID: 12d67756-0618-45d2-bc88-1a6c8d624088
  Args:
    relation: :hasFather
    source: ErnestAugustus
    target: ErnestAugustusOfHanover
  AddTriple (1dcccff7-2b54-4713-afeb-c20fe4364e23)
 Call ID: 1dcccff7-2b54-4713-afeb-c20fe4364e23
  Args:
    target: WilhelmII
    source: VictoriaLouise
    relation: :hasFather
  AssignClass (11d8a8cc-5c5a-41fc-955b-9c7b110c7b16)
 Call ID: 11d8a8cc-5c5a-41fc-955b-9c7b110c7b16
  Args:
    source: WilhelmII
    type: :Man
  AddTriple (5dad4194-92a6-41a8-acf2-3ac39227a638)
 Call ID: 5dad4194-92a6-41a8-acf2-3ac39227a638
  Args:
    relation: :hasChild
    source: ErnestAugustus
    target: PrinceErnestAugustus
  AssignClass (8fcabf74-3731-4594-a206-aea943de398e)
 Call ID: 8fcabf74-3731-4594-a206-aea943de398e
  Args:
    type: :Man
    source: PrinceErnestAugustus
  AddTriple (96f876c8-48b4-47ac-a28c-b11a7b2bf0e0)
 Call ID: 96f876c8-48b4-47ac-a28c-b11a7b2bf0e0
  Args:
    relation: :hasChild
    source: ErnestAugustus
    target: PrincessFrederica
  AssignClass (dd9488f2-f831-4072-8687-11b592fa8d6b)
 Call ID: dd9488f2-f831-4072-8687-11b592fa8d6b
  Args:
    type: :Woman
    source: PrincessFrederica
  AddTriple (91933d63-5104-48b2-8088-7f48757a960c)
 Call ID: 91933d63-5104-48b2-8088-7f48757a960c
  Args:
    source: PrincessFrederica
    target: PrincePaul
    relation: :hasFather
  AssignClass (08853446-9b8f-48dd-a277-8ba0985bc90e)
 Call ID: 08853446-9b8f-48dd-a277-8ba0985bc90e
  Args:
    source: PrincePaul
    type: :Man
  AddLiteral (08c253e5-b093-4ff7-94f8-8ff7c5e349df)
 Call ID: 08c253e5-b093-4ff7-94f8-8ff7c5e349df
  Args:
    source: PrincessFrederica
    literal_value: 1938
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AddTriple (f6e392fa-ae07-468e-9835-6d110c65fb52)
 Call ID: f6e392fa-ae07-468e-9835-6d110c65fb52
  Args:
    target: VictoriaLouise
    source: PrincessFrederica
    relation: :hasMother
  Finish (9c18f814-2001-41df-842a-b7cd127018bb)
 Call ID: 9c18f814-2001-41df-842a-b7cd127018bb
  Args: